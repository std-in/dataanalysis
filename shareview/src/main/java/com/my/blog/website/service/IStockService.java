package com.my.blog.website.service;

import com.github.pagehelper.PageInfo;
import com.my.blog.website.model.Po.Stock;

public interface IStockService {
    /**
     * 发布股票
     * @param stock
     */
    void publish(Stock stock);

    /**
     *查询股票返回多条数据
     * @param p 当前页
     * @param limit 每页条数
     * @return Stock
     */
    PageInfo<Stock> getStock(Integer p, Integer limit);


    /**
     * 根据id或slug获取股票
     *
     * @param id id
     * @return Stock
     */
    Stock getStock(String id);

    /**
     * 根据主键更新
     * @param stock Stock
     */
    void updateContentByCid(Stock stock);


    /**
     * 查询分类/标签下的股票归档
     * @param mid mid
     * @param page page
     * @param limit limit
     * @return Stock
     */
    PageInfo<Stock> getStockCate(Integer mid, int page, int limit);

    /**
     * 搜索、分页
     * @param keyword keyword
     * @param page page
     * @param limit limit
     * @return Stock
     */
    PageInfo<Stock> getStockCate(String keyword,Integer page,Integer limit);

    /**
     * 根据股票代码删除
     * @param stockcode
     */
    void deleteByCid(String stockcode);

    /**
     * 编辑股票
     * @param stock
     */
    void updateArticle(Stock stock);


    /**
     * 更新原有股票的category
     * @param ordinal
     * @param newCatefory
     */
    void updateCategory(String ordinal,String newCatefory);
}
