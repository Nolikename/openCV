//
//  Tracker.m
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "Tracker.h"
#import "PFDataManager.h"

/// 抽象性能追踪器
@interface Tracker()

/// 性能数据写入器
@property(nonatomic, strong)PFDataManager *dataMgr;

@end

/// 抽象性能追踪器
@implementation Tracker

- (instancetype)initWithCaseName:(NSString *)caseName threshold:(NSDictionary *)threshold{
    self = [super init];
    if (self) {
        
        self.dataMgr = [[PFDataManager alloc] initWithCaseName:caseName];
        self.threshold = threshold;
        
    }
    return self;
}

- (void)startTrace{
    
    NSLog(@"屏幕上显示测试的名字");
    
}


- (void)stopTrace{
    NSLog(@"🚀 - 结束追踪");
    NSArray *arr = [self values];
    NSLog(@"🚀 - 性能数据%@", arr);
    [self.dataMgr writeToSandBox: arr];
    
}

- (NSArray *)values{
    return nil;
}

- (void)addStageToIndicator:(NSString *)stageIndex index:(NSString *)index{
    return;
}

- (void)addEndTimeToStage:(NSString *)endTime stageIndex:(NSString *)stageIndex index:(NSString *)index {
    return;
}

- (void)setRecordStartTime{
    [self.dataMgr setRecordStartTime];
}

- (void)setRecordEndTime{
    [self.dataMgr setRecordEndTime];
}

@end
