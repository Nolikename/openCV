//
//  PerfDogTrackerFactory.m
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/3/31.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//


#import "PerfDogTrackerFactory.h"
#import "PerfDogTracker.h"

/// 温度追踪器生产工厂
@implementation PerfDogTrackerFactory

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList{
    return [[PerfDogTracker alloc] initWithCaseName:caseName indexList:indexList];
}

@end
