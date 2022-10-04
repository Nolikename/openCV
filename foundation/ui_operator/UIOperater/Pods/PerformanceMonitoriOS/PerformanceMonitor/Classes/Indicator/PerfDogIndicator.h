//
//  PerfDogIndicator.h
//  PerformanceMonitor
//
//  Created by 李宁 on 2022/3/25.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#import "Indicator.h"
#import "PerfDogConst.h"
#import "Stage.h"


NS_ASSUME_NONNULL_BEGIN


/// PerfDog采集的指标，通用
@interface PerfDogIndicator : Indicator

/// 初始化方法
///  index 指标id 参考PerfDogConst
///  name 指标名
///  threshold 自定义阈值
///  unit
///  calculationMethod 计算方法
///  calculationStage 计算阶段
///  computingPercent 分位值
- (instancetype)initWithIndex:(NSDictionary *)indexInfo;


- (NSDictionary *)template;

- (void)addStage:(NSString *)stageIndex;

- (Stage *)getStageByStageIndex:(NSString *)stageIndex;

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

/// PerfDog指标
- (PerfDogIndex) index;

/// 计算方法
- (CalculationMethod) calculationMethod;

/// 阶段
- (NSString *) calculationStage;

/// 分位
- (int) computingPercent;

@end

NS_ASSUME_NONNULL_END
