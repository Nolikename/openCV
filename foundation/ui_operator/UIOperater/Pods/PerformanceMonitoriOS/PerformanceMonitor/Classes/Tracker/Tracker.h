//
//  Tracker.h
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//
#import "EPDefine.h"
#import "NSDictionary+value.h"

NS_ASSUME_NONNULL_BEGIN
/// 抽象性能追踪器
@interface Tracker : NSObject

/// 开始追踪
-(void)startTrace;

/// 结束追踪
-(void)stopTrace;

/// 模版方法：返回特定格式的字典数组
- (NSArray *)values;

/// 阈值结构体
@property(nonatomic, copy)NSDictionary *threshold;

/// 初始化方法
/// @param caseName 用例名
/// @param threshold 阈值结构体
- (instancetype)initWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold;

- (void)addStageToIndicator:(NSString *)stageIndex index:(NSString *)index;

- (void)addEndTimeToStage:(NSString *)endTime stageIndex:(NSString *)stageIndex index:(NSString *)index;

- (void)setRecordStartTime;

- (void)setRecordEndTime;

@end

NS_ASSUME_NONNULL_END
