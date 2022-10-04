//
//  Factory.h
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "Tracker.h"

NS_ASSUME_NONNULL_BEGIN

/// Tracker抽象工厂类
@interface TrackerFactory : NSObject

typedef NS_ENUM(NSInteger, TrackerType){
    TrackerTypeBasic,  // 基础性能追踪器
    TrackerTypeLaunch,  // 启动速度追踪器
    TrackerTemperature,  // 温度追踪器
    TrackerTypeNetwork // 网络流量
};

+ (instancetype)factoryWithName:(NSString *)factoryName;


- (Tracker *)createTrackerWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold;

- (Tracker *)createTrackerWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList;

@end

NS_ASSUME_NONNULL_END
