//
//  EPTestConfig.m
//  PerformanceMonitorComponent_Example
//
//  Created by henry on 2021/5/26.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "EPTestConfig.h"

/// 配置单例
@interface EPTestConfig()

/// 产品名
@property(nonatomic, copy)NSString *productname;

/// 项目id
@property(nonatomic, copy)NSString *projectId;

@end


/// 配置单例
@implementation EPTestConfig

// 实例
static EPTestConfig* gInstance = nil;

// 单例
+ (instancetype)shareConfig{
    static dispatch_once_t onceToken ;
    dispatch_once(&onceToken, ^{
        gInstance = [[super allocWithZone:NULL] init] ;
    }) ;
    return gInstance ;
}

// allocWithZone
+ (id)allocWithZone:(struct _NSZone *)zone{
    return [EPTestConfig shareConfig] ;
}

// copyWithZone
- (id)copyWithZone:(struct _NSZone *)zone{
    return [EPTestConfig shareConfig] ;
}

// 配置产品名
- (void)configProductName:(NSString *)productname{
    _productname = productname;
}

// 获取产品名
- (NSString *)productName{
    if (!_productname) {
        _productname = @"Unknown ProductName";
    }
    return _productname;
}

// 配置产品名
- (void)configProjectId:(NSString *)projectId{
    _projectId = projectId;
}

// 获取projectId
- (NSString *)projectId{
    if (!_projectId) {
        _projectId = @"Unknown projectId";
    }
    return _projectId;
}

@end
