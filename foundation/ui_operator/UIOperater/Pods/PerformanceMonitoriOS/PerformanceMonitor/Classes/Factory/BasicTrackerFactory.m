//
//  BasicTrackerFactory.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "BasicTrackerFactory.h"
#import "BasicTracker.h"

/// 基础性能追踪器生产工厂
@implementation BasicTrackerFactory

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold{
    return [[BasicTracker alloc] initWithCaseName:caseName threshold:threshold];
}

@end
