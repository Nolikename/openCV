//
//  PFDeviceInfo.h
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

/// 设备信息
@interface PFDeviceInfo : NSObject

/// 操作系统 IPH/AND
+ (NSString *)OS;

/// 操作系统版本
+ (NSString *)OSVersion;

/// 手机版本iPhone12 pro max
+ (NSString *)deviceModel;

/// 汇总OS、OSVersion、deviceModel等信息
+ (NSDictionary *)dicForBaseParam;

/// CPU核数
+ (NSInteger)cpuNum;

@end

NS_ASSUME_NONNULL_END
