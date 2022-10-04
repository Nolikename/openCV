//
//  Indicator.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "Indicator.h"
#import "PFCaculator.h"
#import "EPDefine.h"

/// 性能指标抽象类
@interface Indicator()

/// 指标的值
@property(nonatomic, copy)NSString *values;

/// 指标的阈值
@property(nonatomic, assign)int indicatorThreshold;

@end

/// 性能指标抽象类
@implementation Indicator

- (instancetype)initWithValues:(NSString *)values {
    return [self initWithValues:values indicatorThreshold:0];
}

- (instancetype)initWithValues:(NSString *)values indicatorThreshold:(int)threshold {
    if ([super init]) {
        self.values = values;
        self.indicatorThreshold = threshold;
    }
    return self;
}

- (NSDictionary *)template {
    
    float avg = [PFCaculator avg: self.values];
    float max = [PFCaculator max: self.values];
    float min = [PFCaculator min: self.values];
    
    int threshold = self.indicatorThreshold == -2? [self thresHold] : self.indicatorThreshold;// 如果自定义了阈值就使用自定义的阈值，如果没有就使用指标内的默认配置
    int comparisonMode = [self comparisonMode];
    
    NSString *conclusion = [self determineConclusionWithThreshold:threshold comparisonMode:comparisonMode average:avg];
    NSString *cause = [self determineCauseWithAverage:avg comparisonMode:comparisonMode threshold:threshold];
    
    return @{
        @"Name": [self name],
        @"Threshold": @(threshold),
        @"ComparisonMode": @(comparisonMode),
        @"ThresholdUp": @([self thresholdUp]),
        @"ThresholdDown": @([self thresholdDown]),
        @"Type": @"string",
        @"Value": self.values,
        @"Average": [NSString stringWithFormat:@"%.2f", avg],
        @"MinValue": [NSString stringWithFormat:@"%.2f", min],
        @"MaxValue": [NSString stringWithFormat:@"%.2f", max],
        @"Unit": [self unit],
        @"Conclusion": conclusion,
        @"Cause": cause,
        @"HideChat": @([self hideChat])
    };
}

# pragma mark - 辅助方法
- (NSString *)determineConclusionWithThreshold:(int)threshold comparisonMode:(int)comparisonMode average:(float)avg {
    NSString *conclusion = @"";
    if (threshold == DO_NOT_CARE_THRESHOLD) {
        // -1 表示没有阈值
        conclusion = PASS;
    } else if (comparisonMode == 0) {
        conclusion = threshold >= avg ? PASS: FAIL;
    } else {
        conclusion = avg >= threshold ? PASS: FAIL;
    }
    return conclusion;
}

- (NSString *)determineCauseWithAverage:(float)avg comparisonMode:(int)comparisonMode threshold:(int)threshold {

    NSString *conclusion = [self determineConclusionWithThreshold:threshold comparisonMode:comparisonMode average:avg];

    NSString *cause = @"";
    if ([conclusion isEqualToString:@"fail"]) {
        NSString *lessMoreStr = comparisonMode == 0 ? @"大于": @"小于";
        NSString *ratioStr = @"";
        if (threshold != 0) {
            float percent = fabsf(avg - threshold)/ threshold;
            NSString *floatStr = [NSString stringWithFormat:@"%.2f", percent * 100];
            NSString *floatStrRemoveZero = [self removeFloatAllZeroByString:floatStr];
            ratioStr = [NSString stringWithFormat:@"%@%@",floatStrRemoveZero, @"%"];
        }
        cause = [NSString stringWithFormat:@"%@%@阈值%@", [self name], lessMoreStr, ratioStr];
    } else {
        cause = @"-";
    }
    return cause;
}

- (void)indicatorMethodNotImplemented {
    @throw [NSException exceptionWithName:NSInternalInconsistencyException
                                   reason:[NSString stringWithFormat:@"你必须在子类重写 %@", NSStringFromSelector(_cmd)]
                                 userInfo:nil];
}

# pragma mark - 模版方法,由子类实现
- (NSString *)name {
    [self indicatorMethodNotImplemented];
    return @"";
}

- (int)comparisonMode {
    [self indicatorMethodNotImplemented];
    return 0;
}

- (NSString *)value {
    [self indicatorMethodNotImplemented];
    return @"";
}

- (NSString *)unit {
    [self indicatorMethodNotImplemented];
    return @"";
}

- (int)thresHold {
    [self indicatorMethodNotImplemented];
    return 0;
}

- (int)thresholdDown {
    return 0;
}

-(int)thresholdUp {
    return 0;
}

- (BOOL)hideChat {
    return NO;
}

- (int)getIndicatorThreshold {
    return _indicatorThreshold;
}


/// 去掉小数点后面的无效0
/// @param floatStr 小数字符串
- (NSString*)removeFloatAllZeroByString:(NSString *)floatStr{
    NSString * outNumber = [NSString stringWithFormat:@"%@",@(floatStr.doubleValue)];
    return outNumber;
}

@end
