//
//  TemperatureIndicator.m
//  NextTestTests
//
//  Created by ihenryhuang on 2021/4/8.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "TemperatureIndicator.h"

/// 温度指标
@implementation TemperatureIndicator

/// 设置指标名称
- (NSString *)name{
    return @"温度";
}

/// 设置阈值
- (int)thresHold {
    return 40;
}

/// 允许对比数据比自己低多少个百分点
-(int)thresholdDown {
    return 10;
}

- (int)thresholdUp {
    return 10;
}

/// 值越低越好
- (int)comparisonMode {
    return 0;
}

/// 设置指标的单位
- (NSString *)unit {
    return @" ℃";
}

/// 数据展示不要隐藏图标
- (BOOL)hideChat {
    return NO;
}

@end
