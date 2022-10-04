//
//  NetworkIndicator.m
//  NextTestTests
//
//  Created by wendelli on 2021/4/8.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "NetworkIndicator.h"

/// 网络流量指标
@implementation NetworkIndicator

/// 指标的名称
- (NSString *)name {
    return @"网络流量";
}

/// 指标默认的阈值
- (int)thresHold {
    return 10;
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
    return @"KB/s";
}

@end
