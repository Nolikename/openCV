//
//  NPTFPSScraper.m
//  NextTestTests
//
//  Created by BenArvin on 2019/6/15.
//  Copyright © 2019 Qzone_test. All rights reserved.
//

#import "FPSScraper.h"
#import <QuartzCore/CADisplayLink.h>
#include <mach/mach_time.h>
//#import "NPTHeader.h"
//#import "Performance.h"
//#import "NSValue+BasciPerfThresHoldInfo.h"

/// FPS追踪器
@interface FPSScraper() {
}

/// 是否追踪
@property (atomic) BOOL tracking;

/// 是否停止
@property (atomic) BOOL stopping;

/// displayLink
@property (nonatomic) CADisplayLink *displayLink;

/// frame与frame之间的时间间隔
@property (nonatomic) CFTimeInterval frameDuration;

/// 是不是第一次更新
@property (nonatomic) BOOL firstUpdate;

/// 上次的时间
@property (nonatomic) NSDate *previousTime;

/// 上一frame的时间戳
@property (nonatomic) NSTimeInterval previousFrameTimestamp;

/// 掉帧记录
@property (nonatomic) NSMutableArray *dropFrameRecords;

/// 掉帧间隔记录
@property (nonatomic) NSMutableArray *dropDurationsRecords;

/// 开始记录的时间
@property (nonatomic) NSDate *secStart;

/// 记录到的fps的数量
@property (nonatomic) NSUInteger secFrameCount;

/// 记录到的fps
@property (atomic) NSUInteger secFrame;

/// block
@property (nonatomic) void(^timerBlock)(NSUInteger frame);

/// ⚠️用于暂时存储流畅度数据，供协议方法取用
@property (nonatomic) CGFloat fluencyTmp;

/// 用于存储fps的值
@property (nonatomic,copy) NSString *fpsValue;

@end

/// FPS追踪器
@implementation FPSScraper

- (void)dealloc {
    if (self.displayLink) {
        [self.displayLink invalidate];
    }
}

- (instancetype)init {
    self = [super init];
    if (self) {
        _displayLink = [CADisplayLink displayLinkWithTarget:self selector:@selector(displayLinkAction:)];
        [_displayLink addToRunLoop:[NSRunLoop mainRunLoop] forMode:NSRunLoopCommonModes];
        _displayLink.paused = YES;
        _secFrameCount = 0;
        _secFrame = 60;
    }
    return self;
}

#pragma mark - public methods
- (void)start:(void(^)(NSUInteger frame))timerBlock {
    if (self.tracking) {
        return;
    }
    self.tracking = YES;
    typeof(self) weakSelf = self;
    dispatch_async([[self class] workQueue], ^{
        typeof(weakSelf) strongSelf = weakSelf;
        strongSelf.timerBlock = timerBlock;
        strongSelf.secFrameCount = 0;
        [strongSelf resetDropFrameData];
        strongSelf.firstUpdate = YES;
        strongSelf.secStart = [NSDate date];
        strongSelf.displayLink.paused = NO;
    });
}

- (void)stop:(void(^)(CGFloat fluency))callback {
    if (!self.tracking || self.stopping) {
        if (callback) {
            callback(1.0);
        }
        return;
    }
    self.stopping = YES;
    typeof(self) weakSelf = self;
    dispatch_sync([[self class] workQueue], ^{
        typeof(weakSelf) strongSelf = weakSelf;
        strongSelf.displayLink.paused = YES;
        //        [strongSelf finishTheTailData:[NSDate date]];//MARK: ⚠️由于流畅度公式复用WSQQScrollPerformanceTracker，所以最后时间不做处理
        CGFloat fluencyTmp = [strongSelf calculateFluency];
        strongSelf.fluencyTmp = fluencyTmp;
        strongSelf.tracking = NO;
        strongSelf.stopping = NO;
        if (callback) {
            callback(fluencyTmp);
        }
    });
}

#pragma mark - selector methods
- (void)displayLinkAction:(CADisplayLink *)sender {
    if (!self.tracking) {
        return;
    }
    NSDate *currentTime = [NSDate date];
    CFTimeInterval durationTmp = sender.duration;
    CFTimeInterval timestampTmp = sender.timestamp;
    typeof(self) weakSelf = self;
    dispatch_async([[self class] workQueue], ^{
        typeof(weakSelf) strongSelf = weakSelf;
        [strongSelf timerDataReceiver:currentTime duration:durationTmp timestamp:timestampTmp];
    });
}

#pragma mark - private methods
+ (dispatch_queue_t)workQueue {
    static dispatch_once_t onceToken;
    static dispatch_queue_t workQueue;
    dispatch_once(&onceToken, ^{
        workQueue = dispatch_queue_create("com.NPTFPSScraperTracker.workQueue", DISPATCH_QUEUE_SERIAL);
    });
    return workQueue;
}

+ (dispatch_queue_t)callbackQueue {
    static dispatch_once_t onceToken;
    static dispatch_queue_t callbackQueue;
    dispatch_once(&onceToken, ^{
        callbackQueue = dispatch_queue_create("com.NPTFPSScraperTracker.callbackQueue", DISPATCH_QUEUE_SERIAL);
    });
    return callbackQueue;
}

- (void)timerDataReceiver:(NSDate *)currentTime duration:(CFTimeInterval)duration timestamp:(CFTimeInterval)timestamp {
    if ([currentTime timeIntervalSinceDate:self.secStart] < 1) {
        self.secFrameCount++;
    } else {
        self.secFrame = self.secFrameCount;
        self.secFrameCount = 0;
        self.secStart = currentTime;
        if (self.timerBlock) {
            typeof(self) weakSelf = self;
            dispatch_async([[self class] callbackQueue], ^{
                typeof(weakSelf) strongSelf = weakSelf;
                strongSelf.timerBlock(strongSelf.secFrame);
            });
        }
    }
    
    if (self.firstUpdate) {
        self.firstUpdate = NO;
        self.frameDuration = duration;
        self.secFrame = ceil(1.0 / duration);
        self.previousFrameTimestamp = timestamp;
    } else {
        [self recordDropFrameData:timestamp - self.previousFrameTimestamp];
        self.previousFrameTimestamp = timestamp;
    }
    self.previousTime = currentTime;
}

- (void)resetDropFrameData {
    if (!self.dropFrameRecords) {
        self.dropFrameRecords = [[NSMutableArray alloc] init];
        self.dropDurationsRecords = [[NSMutableArray alloc] init];
    } else {
        [self.dropFrameRecords removeAllObjects];
        [self.dropDurationsRecords removeAllObjects];
    }

    [self.dropFrameRecords addObjectsFromArray:@[@(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0),
                                                 @(0)]];//index 0-16：掉0帧，1帧，2帧，3帧...14帧，15帧，大于15帧
    [self.dropDurationsRecords addObjectsFromArray:@[@(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0),
                                                     @(0)]];
}

- (void)recordDropFrameData:(NSTimeInterval)frameInterval {
    NSInteger dropedFrameCount = ceil(frameInterval / self.frameDuration) - 1;
    NSInteger index = 0;
    if (dropedFrameCount <= 15) {
        index = dropedFrameCount >= 0 ? dropedFrameCount : 0;
    }
    [self.dropFrameRecords replaceObjectAtIndex:index withObject:@((((NSNumber *)[self.dropFrameRecords objectAtIndex:index]).integerValue + 1))];
    NSNumber *dropDurationValue = @((((NSNumber *)[self.dropDurationsRecords objectAtIndex:index]).doubleValue + frameInterval));
    [self.dropDurationsRecords replaceObjectAtIndex:index
                                         withObject:dropDurationValue];
}

- (void)finishTheTailData:(NSDate *)stopDate {
    if (self.firstUpdate) {
        return;
    }
    [self recordDropFrameData:[stopDate timeIntervalSinceDate:self.previousTime]];
}

- (CGFloat)calculateFluency {
    NSInteger zero = ((NSNumber *)[self.dropFrameRecords objectAtIndex:0]).integerValue;
    NSInteger one = ((NSNumber *)[self.dropFrameRecords objectAtIndex:1]).integerValue;
    NSInteger zeroOne = zero + one;
    
    NSInteger two = ((NSNumber *)[self.dropFrameRecords objectAtIndex:2]).integerValue;
    
    NSInteger three = ((NSNumber *)[self.dropFrameRecords objectAtIndex:3]).integerValue;
    NSInteger four = ((NSNumber *)[self.dropFrameRecords objectAtIndex:4]).integerValue;
    NSInteger threeFour = three + four;
    
    NSInteger five = ((NSNumber *)[self.dropFrameRecords objectAtIndex:5]).integerValue;
    NSInteger six = ((NSNumber *)[self.dropFrameRecords objectAtIndex:6]).integerValue;
    NSInteger seven = ((NSNumber *)[self.dropFrameRecords objectAtIndex:7]).integerValue;
    NSInteger eight = ((NSNumber *)[self.dropFrameRecords objectAtIndex:8]).integerValue;
    NSInteger fiveEight = five + six + seven + eight;
    
    CGFloat allDuration = 0.0;
    for (NSNumber *durationItem in self.dropDurationsRecords) {
        allDuration = allDuration + durationItem.doubleValue;
    }
    return (zeroOne + two * 1.5 + threeFour * 3 + fiveEight * 6) * self.frameDuration / allDuration;
}

#pragma mark - NPTScraperProtocal
- (void)startScrape {
    self.fpsValue = @"";
    [self start:nil];
}

- (void)stopScrape {
    [self stop:nil];
}

- (NSNumber *)grabTraceData {
    if (self.fpsValue.length == 0) {
        self.fpsValue = [NSString stringWithFormat:@"%@", @(self.secFrame)];
    } else {
        self.fpsValue = [NSString stringWithFormat:@"%@,%@",self.fpsValue, @(self.secFrame)];
    }
    return @(self.secFrame);
}

@end
