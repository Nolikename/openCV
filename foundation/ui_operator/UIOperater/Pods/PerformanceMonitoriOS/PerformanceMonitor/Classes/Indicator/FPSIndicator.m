//
//  FPSIndicator.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "FPSIndicator.h"

/// FPS指标
@implementation FPSIndicator

/// 指标名称
- (NSString *)name {
    return @"FPS";
}

/// 默认阈值
- (int)thresHold {
    return 58;
}

/// 允许对比数据比自己高多少个百分点
- (int)thresholdUp {
    return 0;
}

/// 值越高越好
- (int)comparisonMode {
    return 1;
}

/// 设置单位
- (NSString *)unit {
    return @"";
}

@end
