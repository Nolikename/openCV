//
//  BasicPerformanceTracker.h
//  PerformanceMonitor
//
//  Created by 李宁 on 2022/3/18.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#import "Tracker.h"

NS_ASSUME_NONNULL_BEGIN
/// PerfDog基础性能追踪器
@interface PerfDogTracker : Tracker

- (instancetype)initWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList;

- (void)addStageToIndicator:(NSString *)stageIndex index:(NSString *)index;

- (void)addEndTimeToStage:(NSString *)endTime stageIndex:(NSString *)stageIndex index:(NSString *)index;

@end

NS_ASSUME_NONNULL_END
