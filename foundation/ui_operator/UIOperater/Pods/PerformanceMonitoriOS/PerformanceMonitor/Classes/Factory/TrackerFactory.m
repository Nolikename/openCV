//
//  Factory.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "TrackerFactory.h"
#import "EPDefine.h"
#import "BasicTrackerFactory.h"
#import "TemperatureTrackerFactory.h"
#import "NetworkTrackerFactory.h"
#import "PerfDogTrackerFactory.h"

/// Tracker抽象工厂类
@implementation TrackerFactory

/// 创建工厂实例
/// @param factoryName 工厂名称
+ (instancetype)factoryWithName:(NSString *)factoryName{
    TrackerFactory *factory = [[NSClassFromString(factoryName) alloc] init];
    return factory;
}

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold{
    return nil;
}


- (Tracker *)createTrackerWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList{
    return nil;
}

@end
