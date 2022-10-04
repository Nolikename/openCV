//
//  NSDictionary+value.h
//  PerfDemo
//
//  Created by henry on 2021/4/23.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "EPDefine.h"

NS_ASSUME_NONNULL_BEGIN

@interface NSDictionary (value)

/// 从字典中获取阈值，如果没有key就返回-2，-2取默认阈值
/// @param key key值
-(int)thresholdWithKey:(NSString *)key;

@end

NS_ASSUME_NONNULL_END
