//
//  MemoryIndicator.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "MemoryIndicator.h"

/// 内存指标
@implementation MemoryIndicator

/// 指标的名称
- (NSString *)name {
    return @"内存占用";
}

/// 指标默认的阈值
- (int)thresHold {
    return 400;
}

/// 允许对比数据比自己低的百分点
- (int)thresholdDown {
    return 10;
}

/// 性能数据越低越好
- (int)comparisonMode {
    return 0;
}

/// 单位
- (NSString *)unit {
    return @"Mb";
}

@end
