//
//  NPTCPUScraper.h
//  Performance
//
//  Created by Iansl on 2019/6/10.
//  Copyright © 2019 Tencent. All rights reserved.
//

#import <UIKit/UIKit.h>

/// CPU追踪器
@interface CPUScraper: NSObject

/// 阈值字典
@property(nonatomic, copy)NSDictionary *thresholdDic;

/// 获取CPU使用率
+ (double)getCpuUsage;

/// 返回 CPU json 数据
- (NSDictionary *)grabTraceData;

@end


