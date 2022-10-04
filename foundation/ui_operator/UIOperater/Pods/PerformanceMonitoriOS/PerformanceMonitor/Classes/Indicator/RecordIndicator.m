//
//  RecordIndicator.m
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/5/6.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "RecordIndicator.h"
#import "PFCaculator.h"

/// 录屏分帧耗时类指标采集的指标，通用
@interface RecordIndicator()

/// 指标命名
@property(nonatomic, copy)NSString *name;

/// 单位
@property(nonatomic, copy)NSString *unit;

/// 计算阶段
@property(nonatomic, copy)NSString *recordStage;

/// 计算分位
@property(nonatomic, assign)int computingPercent;

@end


/// 录屏分帧耗时类指标采集的
@implementation RecordIndicator


- (NSString *)name {
    return _name;
}

- (int)comparisonMode {
    return 0;
}

- (NSString *)value {
    return @"";
}

- (NSString *)unit {
    return _unit;
}

- (int)thresHold {
    return [super getIndicatorThreshold];
}

- (int)thresholdDown {
    return 10;
}

-(int)thresholdUp {
    return 10;
}


- (NSString *) record_stage {
    return _recordStage;
}

- (int) computing_percent {
    return self.computingPercent;
}

- (instancetype)initWithIndex:(NSDictionary *)indexInfo{
    self.name = indexInfo[@"name"];
    self.unit = indexInfo[@"unit"];
    self.recordStage = indexInfo[@"recordStage"];
    self.computingPercent = [[NSString stringWithFormat:@"%@",
                              indexInfo[@"computingPercent"]] intValue];
    
    return [self initWithValues:@"" indicatorThreshold:[[
        NSString stringWithFormat:@"%@", indexInfo[@"threshold"]] intValue]];
}

- (NSDictionary *)template {
    
    float avg = [PFCaculator avg: self.value];
    float max = [PFCaculator max: self.value];
    float min = [PFCaculator min: self.value];
    
    int threshold = self.thresHold;
    int comparisonMode = [self comparisonMode];
    
    NSString *conclusion = [super determineConclusionWithThreshold:threshold comparisonMode:comparisonMode average:avg];
    NSString *cause = [super determineCauseWithAverage:avg comparisonMode:comparisonMode threshold:threshold];
    
    return @{
        @"Name": [self name],
        @"Threshold": @(threshold),
        @"ComparisonMode": @(comparisonMode),
        @"ThresholdUp": @([self thresholdUp]),
        @"ThresholdDown": @([self thresholdDown]),
        @"Type": @"string",
        @"Value": self.value,
        @"Average": [NSString stringWithFormat:@"%.2f", avg],
        @"MinValue": [NSString stringWithFormat:@"%.2f", min],
        @"MaxValue": [NSString stringWithFormat:@"%.2f", max],
        @"Unit": [self unit],
        @"Conclusion": conclusion,
        @"Cause": cause,
        @"HideChat": @([self hideChat]),
        @"recordStage": [self record_stage],
        @"ComputingPercent": @([self computing_percent]),
    };
}

@end
