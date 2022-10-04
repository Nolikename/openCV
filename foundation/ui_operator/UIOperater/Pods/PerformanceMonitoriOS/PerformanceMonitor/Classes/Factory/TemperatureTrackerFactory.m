//
//  TemperatureTrackerFactory.m
//  NextTestTests
//
//  Created by ihenryhuang on 2021/4/8.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "TemperatureTrackerFactory.h"
#import "TemperatureTracker.h"

/// 温度追踪器生产工厂
@implementation TemperatureTrackerFactory

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold{
    return [[TemperatureTracker alloc] initWithCaseName:caseName threshold:threshold];
}

@end
