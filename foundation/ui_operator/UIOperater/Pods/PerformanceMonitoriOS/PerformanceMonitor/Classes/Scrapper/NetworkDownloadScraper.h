//
//  NetworkScraper.h
//  NextTestTests
//
//  Created by wendelli on 2021/4/8.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/// 下行流量追踪器
@interface NetworkDownloadScraper : NSObject

- (instancetype)init;
- (void)startScrape;
- (float)grabTraceData;

@end

NS_ASSUME_NONNULL_END
