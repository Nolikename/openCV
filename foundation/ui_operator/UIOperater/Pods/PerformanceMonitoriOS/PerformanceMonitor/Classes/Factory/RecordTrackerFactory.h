//
//  RecordTrackerFactory.h
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/5/6.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#ifndef RecordTrackerFactory_h
#define RecordTrackerFactory_h


#endif /* RecordTrackerFactory_h */

#import "TrackerFactory.h"

NS_ASSUME_NONNULL_BEGIN

/// 视频录制分帧性能追踪器生产工厂
@interface RecordTrackerFactory : TrackerFactory

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList;

@end

NS_ASSUME_NONNULL_END
