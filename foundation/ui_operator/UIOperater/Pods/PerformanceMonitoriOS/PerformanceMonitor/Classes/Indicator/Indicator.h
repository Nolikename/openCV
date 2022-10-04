//
//  Indicator.h
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/// 性能指标抽象类
@interface Indicator : NSObject

/// 初始化方法
/// @param values 测试出来的指标值
- (instancetype)initWithValues:(NSString *)values;

/// 初始化方法
/// @param values 测试出来的该指标值
/// @param threshold 自定义阈值
- (instancetype)initWithValues:(NSString *)values indicatorThreshold:(int)threshold;

- (NSString *) determineConclusionWithThreshold:(int)threshold comparisonMode:(int)comparisonMode average:(float)avg;

- (NSString *)determineCauseWithAverage:(float)avg comparisonMode:(int)comparisonMode threshold:(int)threshold;

/// 生成数据上报的字典
- (NSDictionary *)template;

#pragma mark - 模版方法，由子类实现
/// 【子类必须重写】指标名称
- (NSString *)name;

/// 【子类必须重写】阈值
- (int)thresHold;

/// 【子类必须重写】指标的数据
- (NSString *)value;

/// 【子类必须重写】单位
- (NSString *)unit;

/// 数据对比的时候允许别人比我高的值，comparisonMode = 1的时候生效
- (int)thresholdUp;

/// 数据对比的时候允许别人比我低的值，comparisonMode = 0的时候生效
- (int)thresholdDown;

/// 指标种类 0:越低越好的指标 1:越高越好的指标
- (int)comparisonMode;

/// 是否隐藏表格
- (BOOL)hideChat;

- (int) getIndicatorThreshold;

@end

NS_ASSUME_NONNULL_END
