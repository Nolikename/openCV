//
//  PFAppInfo.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "PFAppInfo.h"
#import "EPTestConfig.h"

/// App信息
@implementation PFAppInfo

+ (NSString *)productName {
    return [[EPTestConfig shareConfig] productName];
}

/// app显示的名字
+ (NSString *)appName {
    NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
    NSString *appName = [infoDictionary objectForKey:@"CFBundleDisplayName"];
    if ([appName containsString:@"Kwai"]) {
        appName=@"快手";
    }
    return appName;
}

/// 应用的发布版本号
+ (NSString *)appVersion {
    NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
    return [infoDictionary objectForKey:@"CFBundleShortVersionString"];
}

/// 标识内部版本号
+ (NSString *)appBuildVersion {
    NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
    return [infoDictionary objectForKey:@"CFBundleVersion"];
}

@end
