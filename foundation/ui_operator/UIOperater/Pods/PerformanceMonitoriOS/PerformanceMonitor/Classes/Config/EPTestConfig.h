//
//  EPTestConfig.h
//  PerformanceMonitorComponent_Example
//
//  Created by henry on 2021/5/26.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/// 全局配置类
@interface EPTestConfig : NSObject

/// 单例
+ (instancetype)shareConfig;

/// 项目在EPTest上的项目名
/// @param productname 项目名
- (void)configProductName:(NSString *)productname;

/// 获取ProductName
- (NSString *)productName;

/// 项目在EPTest上的项目名
/// @param projectId EPTest上的projectId
- (void)configProjectId:(NSString *)projectId;

/// 获取ProductName
- (NSString *)projectId;

@end

NS_ASSUME_NONNULL_END
