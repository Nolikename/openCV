//
//  NSDictionary+value.m
//  PerfDemo
//
//  Created by henry on 2021/4/23.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "NSDictionary+value.h"


@implementation NSDictionary (value)

- (int)thresholdWithKey:(NSString *)key{
    id value = [self objectForKey:key];
    if(value) {
        return [value intValue];
    } else { // 未设置阈值
        return SET_NO_THRESHOLD;
    }
}
@end
