//
//  PerfDogIndicator.m
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/3/25.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#import <Foundation/Foundation.h>


#import "PerfDogIndicator.h"
#import "PerfDogConst.h"
#import "PFCaculator.h"

@interface PerfDogIndicator()

/// 指标
@property(nonatomic, copy)PerfDogIndex index;

/// 指标命名
@property(nonatomic, copy)NSString *name;

/// 单位
@property(nonatomic, copy)NSString *unit;

/// 计算方法
@property(nonatomic, copy)CalculationMethod calculationMethod;

/// 计算阶段
@property(nonatomic, copy)NSString *calculationStage;

/// 计算分位
@property(nonatomic, assign)int computingPercent;

/// 取时阶段
@property(nonatomic, strong)NSMutableDictionary *testStageList;

@end

/// 性能狗采集
@implementation PerfDogIndicator


- (NSString *)name {
    return _name;
}

- (int)comparisonMode {
    if ([self index] == PerfDogIndexFps) {
        return 1;
    }
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

- (PerfDogIndex) index {
    return _index;
}

- (CalculationMethod) calculation_method {
    return _calculationMethod;
}

- (NSString *) calculation_stage {
    return _calculationStage;
}

- (int) computing_percent {
    return self.computingPercent;
}

- (instancetype)initWithIndex:(NSDictionary *)indexInfo{
    self.index = indexInfo[@"index"];
    self.name = indexInfo[@"name"];
    self.unit = indexInfo[@"unit"];
    self.calculationMethod = indexInfo[@"calculationMethod"];
    self.calculationStage = indexInfo[@"calculationStage"];
    self.computingPercent = [[NSString stringWithFormat:@"%@",
                              indexInfo[@"computingPercent"]] intValue];
    self.testStageList = [[NSMutableDictionary alloc] init];
    
    return [self initWithValues:@"" indicatorThreshold:[[
        NSString stringWithFormat:@"%@", indexInfo[@"threshold"]] intValue]];
}

- (void)addStage:(NSString *)stageIndex{
    [self.testStageList setObject: [[Stage alloc] initWithStageIndex:stageIndex]  forKey:stageIndex];
}

- (Stage *)getStageByStageIndex:(NSString *)stageIndex{
    return [self.testStageList objectForKey:stageIndex];
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
        @"Index": [self index],
        @"CalculationMethod": [self calculation_method],
        @"CalculationStage": [self calculation_stage],
        @"ComputingPercent": @([self computing_percent]),
        @"TestStageList":[self testStageList]
    };
}

@end
