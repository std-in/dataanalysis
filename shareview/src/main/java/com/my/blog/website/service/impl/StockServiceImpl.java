package com.my.blog.website.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.my.blog.website.constant.WebConst;
import com.my.blog.website.dao.MetaVoMapper;
import com.my.blog.website.dao.StockMapper;
import com.my.blog.website.dto.Types;
import com.my.blog.website.exception.TipException;
import com.my.blog.website.model.Po.Stock;
import com.my.blog.website.service.IMetaService;
import com.my.blog.website.service.IRelationshipService;
import com.my.blog.website.service.IStockService;
import com.my.blog.website.utils.DateKit;
import com.my.blog.website.utils.TaleUtils;
import com.my.blog.website.utils.Tools;
import com.vdurmont.emoji.EmojiParser;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class StockServiceImpl implements IStockService {
    private static final Logger LOGGER = LoggerFactory.getLogger(StockServiceImpl.class);

    @Resource
    private StockMapper stockDao;

    @Resource
    private MetaVoMapper metaDao;

    @Resource
    private IRelationshipService relationshipService;

    @Resource
    private IMetaService metasService;

    @Override
    public void publish(Stock stock) {
        if (null == stock) {
            throw new TipException("股票对象为空");
        }
        if (StringUtils.isBlank(stock.getTitle())) {
            throw new TipException("股票标题不能为空");
        }
        if (StringUtils.isBlank(stock.getContent())) {
            throw new TipException("股票内容不能为空");
        }
        int titleLength = stock.getTitle().length();
        if (titleLength > WebConst.MAX_TITLE_COUNT) {
            throw new TipException("股票标题过长");
        }
        int contentLength = stock.getContent().length();
        if (contentLength > WebConst.MAX_TEXT_COUNT) {
            throw new TipException("股票内容过长");
        }
        if (null == stock.getAuthorId()) {
            throw new TipException("请登录后发布股票");
        }
        if (StringUtils.isNotBlank(stock.getSlug())) {
            if (stock.getSlug().length() < 5) {
                throw new TipException("路径太短了");
            }
            if (!TaleUtils.isPath(stock.getSlug())) throw new TipException("您输入的路径不合法");
//            StockExample StockExample = new StockExample();
//            StockExample.createCriteria().andTypeEqualTo(stock.getType()).andStatusEqualTo(stock.getSlug());
//            long count = contentDao.countByExample(StockExample);
//            if (count > 0) throw new TipException("该路径已经存在，请重新输入");
        } else {
            stock.setSlug(null);
        }

        stock.setContent(EmojiParser.parseToAliases(stock.getContent()));

        int time = DateKit.getCurrentUnixTime();
        stock.setCreated(time);
        stock.setModified(time);
        stock.setHits(0);
        stock.setCommentsNum(0);

        String tags = stock.getTags();
        String categories = stock.getCategories();
        stockDao.insert(stock);
        String stockcode = stock.getStockcode();

        metasService.saveMetas(stockcode, tags, Types.TAG.getType());
        metasService.saveMetas(stockcode, categories, Types.CATEGORY.getType());
    }

    @Override
    public PageInfo<Stock> getStock(Integer p, Integer limit) {
        LOGGER.debug("Enter getstock method");
//        StockExample example = new StockExample();
//        example.setOrderByClause("created desc");
//        example.createCriteria().andTypeEqualTo(Types.ARTICLE.getType()).andStatusEqualTo(Types.PUBLISH.getType());
//        PageHelper.startPage(p, limit);
//        List<Stock> data = contentDao.selectByExampleWithBLOBs(example);
//        PageInfo<Stock> pageInfo = new PageInfo<>(data);
//        LOGGER.debug("Exit getstock method");
        return pageInfo;
    }

    @Override
    public Stock getstock(String id) {
        if (StringUtils.isNotBlank(id)) {
            if (Tools.isNumber(id)) {
                Stock Stock = contentDao.selectByPrimaryKey(Integer.valueOf(id));
                if (Stock != null) {
                    Stock.setHits(Stock.getHits() + 1);
                    contentDao.updateByPrimaryKey(Stock);
                }
                return Stock;
            } else {
                StockExample StockExample = new StockExample();
                StockExample.createCriteria().andSlugEqualTo(id);
                List<Stock> Stocks = contentDao.selectByExampleWithBLOBs(StockExample);
                if (Stocks.size() != 1) {
                    throw new TipException("query content by id and return is not one");
                }
                return Stocks.get(0);
            }
        }
        return null;
    }

    @Override
    public void updateContentByCid(Stock Stock) {
        if (null != Stock && null != Stock.getCid()) {
            contentDao.updateByPrimaryKeySelective(Stock);
        }
    }

    @Override
    public PageInfo<Stock> getArticles(Integer mid, int page, int limit) {
        int total = metaDao.countWithSql(mid);
        PageHelper.startPage(page, limit);
        List<Stock> list = contentDao.findByCatalog(mid);
        PageInfo<Stock> paginator = new PageInfo<>(list);
        paginator.setTotal(total);
        return paginator;
    }

    @Override
    public PageInfo<Stock> getArticles(String keyword, Integer page, Integer limit) {
        PageHelper.startPage(page, limit);
        StockExample StockExample = new StockExample();
        StockExample.Criteria criteria = StockExample.createCriteria();
        criteria.andTypeEqualTo(Types.ARTICLE.getType());
        criteria.andStatusEqualTo(Types.PUBLISH.getType());
        criteria.andTitleLike("%" + keyword + "%");
        StockExample.setOrderByClause("created desc");
        List<Stock> Stocks = contentDao.selectByExampleWithBLOBs(StockExample);
        return new PageInfo<>(Stocks);
    }

    @Override
    public PageInfo<Stock> getArticlesWithpage(StockExample commentVoExample, Integer page, Integer limit) {
        PageHelper.startPage(page, limit);
        List<Stock> Stocks = contentDao.selectByExampleWithBLOBs(commentVoExample);
        return new PageInfo<>(Stocks);
    }

    @Override
    public void deleteByCid(Integer cid) {
        Stock stock = this.getstock(cid + "");
        if (null != stock) {
            contentDao.deleteByPrimaryKey(cid);
            relationshipService.deleteById(cid, null);
        }
    }

    @Override
    public void updateCategory(String ordinal, String newCatefory) {
        Stock Stock = new Stock();
        Stock.setCategories(newCatefory);
        StockExample example = new StockExample();
        example.createCriteria().andCategoriesEqualTo(ordinal);
        contentDao.updateByExampleSelective(Stock, example);
    }

    @Override
    public void updateArticle(Stock stock) {
        if (null == stock || null == stock.getCid()) {
            throw new TipException("文章对象不能为空");
        }
        if (StringUtils.isBlank(stock.getTitle())) {
            throw new TipException("文章标题不能为空");
        }
        if (StringUtils.isBlank(stock.getContent())) {
            throw new TipException("文章内容不能为空");
        }
        if (stock.getTitle().length() > 200) {
            throw new TipException("文章标题过长");
        }
        if (stock.getContent().length() > 65000) {
            throw new TipException("文章内容过长");
        }
        if (null == stock.getAuthorId()) {
            throw new TipException("请登录后发布文章");
        }
        if (StringUtils.isBlank(stock.getSlug())) {
            stock.setSlug(null);
        }
        int time = DateKit.getCurrentUnixTime();
        stock.setModified(time);
        Integer cid = stock.getCid();
        stock.setContent(EmojiParser.parseToAliases(stock.getContent()));

        contentDao.updateByPrimaryKeySelective(stock);
        relationshipService.deleteById(cid, null);
        metasService.saveMetas(cid, stock.getTags(), Types.TAG.getType());
        metasService.saveMetas(cid, stock.getCategories(), Types.CATEGORY.getType());
    }
}
