//
//  BasicTracker.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "BasicTracker.h"
#import "CPUIndicator.h"
#import "FPSIndicator.h"
#import "MemoryIndicator.h"
#import "FPSScraper.h"
#import "CPUScraper.h"
#import "MemScraper.h"
#import "NSString+append.h"

/// 基础性能追踪器（cpu/mem/fps）
@interface BasicTracker()

/// 定时器
@property (nonatomic, strong) dispatch_source_t timer;

/// 获取fps的Scraper
@property(nonatomic, strong)FPSScraper *fpsSp;

/// 获取Memory的Scraper
@property(nonatomic, strong)MemScraper *memSp;

/// 性能追踪期间存储fps的值
@property(nonatomic, strong)NSString *fpsValues;

/// 性能追踪期间存储cpu的值
@property(nonatomic, strong)NSString *cpuValues;

/// 性能追踪期间存储mem的值
@property(nonatomic, strong)NSString *memValues;


@end


/// 基础性能追踪器（cpu/mem/fps）
@implementation BasicTracker

- (instancetype)initWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold{
    if ([super initWithCaseName:caseName threshold:threshold]) {
        self.fpsSp = [[FPSScraper alloc] init];
        self.memSp = [[MemScraper alloc] init];
        self.fpsValues = @"";
        self.cpuValues = @"";
        self.memValues = @"";
    }
    return self;
}

- (void)startTrace{
    [super startTrace];
    NSLog(@"🚀 - 开始追踪基础性能");
    
    dispatch_queue_t queue2 = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
    _timer = dispatch_source_create(DISPATCH_SOURCE_TYPE_TIMER, 0, 0, queue2);
    dispatch_source_set_timer(_timer, dispatch_walltime(nil, 0), 1*1000*NSEC_PER_MSEC, 0);
    dispatch_source_set_event_handler(_timer, ^{
        NSNumber *fps = [self.fpsSp grabTraceData];
        self.fpsValues = [self.fpsValues append:[fps floatValue]];
        double usg = [CPUScraper getCpuUsage];
        self.cpuValues = [self.cpuValues append:usg];
        float mem = [MemScraper grabMemoryInfo];
        self.memValues = [self.memValues append:mem];
    });
    dispatch_resume(_timer);
    
}

-(void)stopTrace{
    dispatch_source_cancel(_timer);
    [super stopTrace];
}

- (NSArray *)values{
    
    NSDictionary *ths = self.threshold;
    
    NSArray *resultArr = @[
        
        [[[CPUIndicator alloc] initWithValues:self.cpuValues indicatorThreshold:[ths thresholdWithKey:@"cpu"]] template],
        [[[FPSIndicator alloc] initWithValues:self.fpsValues indicatorThreshold:[ths thresholdWithKey:@"fps"]] template],
        [[[MemoryIndicator alloc] initWithValues:self.memValues indicatorThreshold:[ths thresholdWithKey:@"mem"]] template]
        
    ];
    return resultArr;
    
}

@end
