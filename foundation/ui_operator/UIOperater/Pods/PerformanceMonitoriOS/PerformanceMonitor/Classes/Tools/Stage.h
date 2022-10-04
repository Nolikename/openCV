//
//  Stage.h
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/3/31.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#ifndef Stage_h
#define Stage_h


#endif /* Stage_h */
@interface Stage:NSObject

/// 初始化 传入阶段id
- (instancetype) initWithStageIndex:(NSString *)stageIndex;

/// 添加结束阶段时间戳
- (void) addEnd:(NSString *)end;

- (NSDictionary *) getStage;

- (NSString *) getStageIndex;

+ (NSString *) getTimeNow:(NSString *)timeNow;

@end;
