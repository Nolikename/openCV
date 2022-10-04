//
//  NPTFPSScraper.h
//  NextTestTests
//
//  Created by BenArvin on 2019/6/15.
//  Copyright © 2019 Qzone_test. All rights reserved.
//

#import <UIKit/UIKit.h>

/// FPS数据追踪器
@interface FPSScraper : NSObject
- (void)startScrape;
- (void)stopScrape;
- (NSNumber *)grabTraceData;
@end
