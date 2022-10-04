//
//  TemperatureTracker.m
//  NextTestTests
//
//  Created by ihenryhuang on 2021/3/31.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "TemperatureTracker.h"
#import "TemperatureIndicator.h"

/// 温度追踪器
@interface TemperatureTracker()

@end


/// 温度追踪器
@implementation TemperatureTracker

- (void)startTrace{
    [super startTrace];
    NSLog(@"🚀 - 开始追踪温度");
}

- (void)stopTrace{
    [super stopTrace];
}

- (NSArray *)values{
    NSDictionary *ths = self.threshold;

    NSArray *resultArr = @[
        [[[TemperatureIndicator alloc] initWithValues:@"0" indicatorThreshold:[ths thresholdWithKey:@"temperature"]] template],
    ];
    return resultArr;
}

@end
