//
//  PerfDogTrackerFactory.h
//  PerformanceMonitor
//
//  Created by 李宁 on 2022/3/31.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#ifndef PerfDogTrackerFactory_h
#define PerfDogTrackerFactory_h


#endif /* PerfDogTrackerFactory_h */

#import "TrackerFactory.h"

NS_ASSUME_NONNULL_BEGIN

/// PerfDog性能追踪器生产工厂
@interface PerfDogTrackerFactory : TrackerFactory

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList;

@end

NS_ASSUME_NONNULL_END
