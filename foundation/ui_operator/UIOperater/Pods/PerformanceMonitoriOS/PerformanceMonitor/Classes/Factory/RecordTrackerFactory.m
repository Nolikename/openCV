//
//  RecordTrackerFactory.m
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/5/6.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#import "RecordTrackerFactory.h"
#import "RecordTracker.h"

/// 温度追踪器生产工厂
@implementation RecordTrackerFactory

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList{
    return [[RecordTracker alloc] initWithCaseName:caseName indexList:indexList];
}

@end
