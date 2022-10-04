//
//  NetworkTracker.m
//  NextTestTests
//
//  Created by wendelli on 2021/4/8.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "NetworkTracker.h"
#import "NetworkDownloadScraper.h"
#import "BasicTracker.h"
#import "NetworkIndicator.h"
#import "NSString+append.h"
#import "DMNetworkTrafficManager.h"

/// 网络流量追踪器（download/upload）
@interface NetworkTracker()

/// 定时器
@property (nonatomic, strong) dispatch_source_t timer;

/// 获取network download的scraper
@property(nonatomic, strong)NetworkDownloadScraper *netDownSp;

/// 性能追踪期间存储download的值
@property(nonatomic, strong)NSString *downloadValues;

@end

/// 网络流量追踪器（download/upload）
@implementation NetworkTracker

- (instancetype)initWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold {
    if ([super initWithCaseName:caseName threshold:threshold]) {
        self.netDownSp = [[NetworkDownloadScraper alloc] init];
        self.downloadValues = @"";
    }
    return self;
}

- (void)startTrace {
    [super startTrace];
    NSLog(@"🚀 - 开始追踪网络流量");
    
    [DMNetworkTrafficManager start];
    
    // 每秒钟获取一次网速
    dispatch_queue_t queue2 = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
    _timer = dispatch_source_create(DISPATCH_SOURCE_TYPE_TIMER, 0, 0, queue2);
    dispatch_source_set_timer(_timer, dispatch_walltime(nil, 0), 1 * 1000 * NSEC_PER_MSEC, 0);
    dispatch_source_set_event_handler(_timer, ^{
        float downValues = [self.netDownSp grabTraceData];
        self.downloadValues = [self.downloadValues append:downValues];
    });
    dispatch_resume(_timer);
}

- (void)stopTrace {
    [super stopTrace];
    
    [DMNetworkTrafficManager end];
    dispatch_source_cancel(_timer);
}

- (NSArray *)values {
    NSDictionary *ths = self.threshold;
    NSArray *resultArr = @[
        [[[NetworkIndicator alloc] initWithValues:self.downloadValues indicatorThreshold:[ths thresholdWithKey:@"net"]] template]
    ];
    return resultArr;
}

- (void)dealloc {}

@end
