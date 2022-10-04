//
//  RecordTracker.m
//  PerformanceMonitor_Example
//
//  Created by 李宁 on 2022/5/6.
//  Copyright © 2022 bbc6bae9. All rights reserved.
//

#import "RecordTracker.h"
#import "RecordIndicator.h"
/// 视频录制切帧耗时类测试
@interface RecordTracker()

@property(nonatomic, strong)NSMutableDictionary *IndexList;

@end


/// 视频录制切帧耗时类测试追踪器
@implementation RecordTracker

- (void)startTrace{
    [super startTrace];
    NSLog(@"🚀 - 开始追踪基础性能");
}

- (void)stopTrace{
    [super stopTrace];
}

- (instancetype)initWithCaseName:(NSString *)caseName indexList:(NSArray *)indexList {
    if ([super initWithCaseName:caseName threshold:@{}]) {
        if (self.IndexList == nil) {
            self.IndexList = [[NSMutableDictionary alloc] init];
        }
        for (int i = 0; i < indexList.count; i++) {
            [self.IndexList setObject:[[
                RecordIndicator alloc] initWithIndex:indexList[i]] forKey:indexList[i][@"name"]];
        }
    }
    return self;
}

/// 设置录制开始时间
- (void) setRecordStartTime {
    [super setRecordStartTime];
}

/// 设置录制结束时间
- (void) setRecordEndTime {
    [super setRecordEndTime];
}

- (NSArray *)values{
    NSArray *resultArr = [[NSArray alloc] init];
    
    for(id key in self.IndexList) {
        resultArr = [resultArr arrayByAddingObject:[[self.IndexList objectForKey:key] template]];
    }
    return resultArr;
}

@end
