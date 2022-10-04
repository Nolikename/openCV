//
//  Stage.m
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/3/30.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Stage.h"
@interface Stage()

/// 本阶段开始采集的时间戳
@property(nonatomic, copy) NSString *start;

/// 本阶段结束采集的时间戳
@property(nonatomic, copy) NSString *end;

/// 阶段index 从"1"开始, "2"类似 可跳阶段，但是不能重复
@property(nonatomic, assign) NSString *stageIndex;


@end;

@implementation Stage

- (instancetype) initWithStageIndex:(NSString *)stageIndex{
    self.start = [Stage getTimeNow:@""];
    self.stageIndex = stageIndex;
    return self;
}

- (void) addEnd:(NSString *)end{
    self.end = [Stage getTimeNow:end];
}

+ (NSString *) getTimeNow:(NSString *)timeNow {
    if ([timeNow  isEqual: @""]) {
        UInt64 timestamp = [[NSDate date] timeIntervalSince1970] * 1000;
        timeNow =  [NSString stringWithFormat:@"%llu", timestamp];
    }
    return timeNow;
}

- (NSDictionary *) getStage{
    return @{
        @"Start": [self start],
        @"End": [self end],
        @"StageIndex": [self stageIndex]
    };
}

- (NSString *) getStageIndex{
    return _stageIndex;
}

@end

