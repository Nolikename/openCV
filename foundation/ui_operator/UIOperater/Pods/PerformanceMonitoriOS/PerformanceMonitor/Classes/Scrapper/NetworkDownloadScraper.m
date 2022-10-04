//
//  NetworkScraper.m
//  NextTestTests
//
//  Created by wendelli on 2021/4/8.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "NetworkDownloadScraper.h"
#import "DMDataManager.h"
//#import "NPTHeader.h"

/// 下行流量追踪器
@interface NetworkDownloadScraper()

/// 上次接收下行网络的流量
@property(nonatomic, assign)long long int lastSecondRev;

@end

/// 下行流量追踪器
@implementation NetworkDownloadScraper

- (instancetype)init {
    self = [super init];
    if (self) {
        [self startScrape];
    }
    return self;
}

- (void)startScrape {
    self.lastSecondRev = 0;
}

- (float)grabTraceData {
    long long int incrementRevByteLastSecond = [DMDataManager defaultDB].totalRev - self.lastSecondRev;
    self.lastSecondRev = [DMDataManager defaultDB].totalRev;
    float revSpeed = incrementRevByteLastSecond / 1024; 
    NSLog(@"下行网速 %.2f", revSpeed);
    return revSpeed;
}

@end
