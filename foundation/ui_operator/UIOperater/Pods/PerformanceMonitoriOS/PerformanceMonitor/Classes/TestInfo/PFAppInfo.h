//
//  PFAppInfo.h
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/// App信息
@interface PFAppInfo : NSObject

/*
 产品族的名字
 */
+ (NSString *)productName;

/// app显示的名字
+ (NSString *)appName;

/// 应用的发布版本号
+ (NSString *)appVersion;

/// 标识内部版本号
+ (NSString *)appBuildVersion;

@end

NS_ASSUME_NONNULL_END
