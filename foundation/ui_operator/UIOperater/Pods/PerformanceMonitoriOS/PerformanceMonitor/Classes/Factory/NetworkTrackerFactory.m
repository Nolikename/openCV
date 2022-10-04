//
//  NetworkTrackerFactory.m
//  NextTestTests
//
//  Created by wendelli on 2021/4/8.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "NetworkTrackerFactory.h"
#import "NetworkTracker.h"

/// 流量追踪器生产工厂
@implementation NetworkTrackerFactory

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold{
    return [[NetworkTracker alloc] initWithCaseName:caseName threshold:threshold];
}

@end
