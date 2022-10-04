//
//  RecordIndicator.h
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/5/6.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#ifndef RecordIndicator_h
#define RecordIndicator_h


#endif /* RecordIndicator_h */

#import "Indicator.h"
#import "Stage.h"


NS_ASSUME_NONNULL_BEGIN


/// 录屏分帧耗时类指标采集的指标，通用
@interface RecordIndicator : Indicator

/// 初始化方法
///  name 指标名
///  threshold 自定义阈值
///  unit
///  recordStage 计算阶段
///  computingPercent 分位值计算
- (instancetype)initWithIndex:(NSDictionary *)indexInfo;


- (NSDictionary *)template;

/// 指标名称
- (NSString *)name;

/// 阈值
- (int)thresHold;

/// 指标的数据
- (NSString *)value;

/// 单位
- (NSString *)unit;

/// 数据对比的时候允许别人比我高的值，comparisonMode = 1的时候生效
- (int)thresholdUp;

/// 数据对比的时候允许别人比我低的值，comparisonMode = 0的时候生效
- (int)thresholdDown;

/// 指标种类 0:越低越好的指标 1:越高越好的指标
- (int)comparisonMode;

/// 阶段
- (NSString *) recordStage;

/// 分位
- (int) computingPercent;

@end

NS_ASSUME_NONNULL_END
