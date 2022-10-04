//
//  NSString+append.m
//  Demo
//
//  Created by ihenryhuang on 2021/4/2.
//  Copyright © 2021 Tencent. All rights reserved.
//

#import "NSString+append.h"

@implementation NSString (append)

- (NSString *)append:(float)number {
    NSString *str = self;
    if (self.length == 0) {
        str = [NSString stringWithFormat:@"%.f", number];
    }else{
        str = [NSString stringWithFormat:@"%@,%.f", str, number];
    }
    return str;
}

@end
