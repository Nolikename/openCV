//
//  DataManager.h
//  PerformanceMicrovision
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "PFTestInfo.h"
#import "Stage.h"

NS_ASSUME_NONNULL_BEGIN

/// 性能数据写入器
@interface PFDataManager : NSObject

/// 自定义初始化
/// @param caseName 测试用例名称
- (instancetype)initWithCaseName:(NSString *)caseName;

/// 清除本地所有的轨迹文件
+ (void)cleanAllTraceFile;

/// 将日志写入沙盒
/// @param arr 指标结果数组
- (void)writeToSandBox:(NSArray *)arr;

- (void)setRecordStartTime;

- (void)setRecordEndTime;

@end

NS_ASSUME_NONNULL_END
