//
//  NPTMemScraper.h
//  NextTestTests
//
//  Created by BenArvin on 2019/6/15.
//  Copyright © 2019 Qzone_test. All rights reserved.
//

#import <Foundation/Foundation.h>

/// 内存追踪器
@interface MemScraper : NSObject

/// 抓取内存占用信息
+ (float)grabMemoryInfo;

@end
