//
//  Header.h
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/5/6.
//  Copyright © 2022 bbc6bae9. All rights reserved.

#import "Tracker.h"

NS_ASSUME_NONNULL_BEGIN
/// 视频录制切帧耗时类测试
@interface RecordTracker : Tracker

- (instancetype)initWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList;

/// 设置录制开始时间
- (void) setRecordStartTime;

/// 设置录制结束时间
- (void) setRecordEndTime;

@end

NS_ASSUME_NONNULL_END
