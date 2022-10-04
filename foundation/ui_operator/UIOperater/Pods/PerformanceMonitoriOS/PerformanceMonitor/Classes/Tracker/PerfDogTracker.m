//
//  PerfDogTracker.m
//  PerformanceMonitor
//
//  Created by 李宁 on 2022/3/18.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//


#import "PerfDogTracker.h"
#import "PerfDogIndicator.h"
/// PerfDog基础性能追踪器
@interface PerfDogTracker()

/// perfdog指标列表
@property(nonatomic, strong)NSMutableDictionary *perfDogIndexList;

@end


/// PerfDog基础性能追踪器
@implementation PerfDogTracker

- (void)startTrace{
    [super startTrace];
    NSLog(@"🚀 - 开始追踪基础性能");
}

- (void)stopTrace{
    [super stopTrace];
}

- (instancetype)initWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList {
    if ([super initWithCaseName:caseName threshold:@{}]) {
        if (self.perfDogIndexList == nil) {
            self.perfDogIndexList = [[NSMutableDictionary alloc] init];
        }
        for (int i = 0; i < indexList.count; i++) {
            [self.perfDogIndexList setObject:[[
                PerfDogIndicator alloc] initWithIndex:indexList[i]] forKey:indexList[i][@"index"]];
        }
    }
    return self;
}

/// 添加stage
- (void)addStageToIndicator:(NSString *)stageIndex index:(NSString *)index {
    if ([index isEqual: @""]) {
        for(id key in self.perfDogIndexList) {
            [[self.perfDogIndexList objectForKey:key] addStage:stageIndex];
        }
    }
    [[self.perfDogIndexList objectForKey:index] addStage:stageIndex];
}

- (void)addEndTimeToStage:(NSString *)endTime stageIndex:(NSString *)stageIndex index:(NSString *)index {
    if ([index isEqual: @""]) {
        for(id key in self.perfDogIndexList) {
            [[[self.perfDogIndexList objectForKey:key] getStageByStageIndex:stageIndex] addEnd:endTime];
        }
    }
    [[[self.perfDogIndexList objectForKey:index] getStageByStageIndex:stageIndex] addEnd:endTime];
}

- (NSArray *)values{
    NSArray *resultArr = [[NSArray alloc] init];
    
    for(id key in self.perfDogIndexList) {
        resultArr = [resultArr arrayByAddingObject:[[self.perfDogIndexList objectForKey:key] template]];
    }
    return resultArr;
}

@end
