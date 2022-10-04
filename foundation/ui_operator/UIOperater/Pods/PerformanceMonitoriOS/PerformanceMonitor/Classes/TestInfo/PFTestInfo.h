//
//  PFTestInfo.h
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//
#import <Foundation/Foundation.h>
NS_ASSUME_NONNULL_BEGIN
/// 测试信息
@interface PFTestInfo : NSObject
/// 产品名称
@property (nonatomic) NSString *productName;
/// 性能测试用例名称
@property (nonatomic) NSString *caseName;
/// app名称
@property (nonatomic) NSString *appName;
/// app版本
@property (nonatomic) NSString *appVersion;
/// app构建号
@property (nonatomic) NSInteger appBuildNum;
/// 操作系统
@property (nonatomic) NSString *OS;
/// 操作系统版本信息
@property (nonatomic) NSString *OSVersion;
/// 设备信息
@property (nonatomic) NSString *deviceModel;
/// 开始时间
@property (nonatomic) NSInteger startTime; //启动时间，unix1970时间戳，精度到s
/// 录屏分帧类开始时间
@property (nonatomic) NSString *RecordStartTime;
/// 录屏分帧类结束时间
@property (nonatomic) NSString *RecordEndTime;

/// 初始化方法
/// @param caseName 测试用例名称
- (instancetype)initWithCaseName:(NSString *)caseName;

/// 设置录屏分帧开始时间
- (void) setRecordStartTime;

/// 设置录屏分帧结束时间
- (void) setRecordEndTime;

@end

NS_ASSUME_NONNULL_END
 
