package com.my.blog.website.dao;

import com.my.blog.website.model.Bo.ArchiveBo;
import com.my.blog.website.model.Po.Stock;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public interface StockMapper {

    int deleteByPrimaryKey(String stockcode);

    int insert(Stock stock);

    int insertSelective(Stock stock);

    Stock selectByPrimaryKey(String stockcode);

    int updateByPrimaryKeySelective(Stock stock);

    int updateByPrimaryKeyWithBLOBs(Stock stock);

    int updateByPrimaryKey(Stock stock);

    List<ArchiveBo> findReturnArchiveBo();

    List<Stock> findByCatalog(String stockcode);
}
