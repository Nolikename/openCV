//
//  Caculator.m
//  NextTestDylib
//
//  Created by ihenryhuang(黄洪) on 2020/11/8.
//  Copyright (c) 2021年 Tencent. All rights reserved.
//

#import "PFCaculator.h"

/**
  计算values的平均值的计算器
 */
@implementation PFCaculator

+ (float)avg:(NSString *)valueStr {
    if (![PFCaculator isDataValid:valueStr]) {
        return  -1;
    }
    NSArray *array = [valueStr componentsSeparatedByString:@","];
    
    float avg = [[array valueForKeyPath:@"@avg.floatValue"] floatValue];
    
    return avg;
}

+ (BOOL)isDataValid:(NSString *)checkString {
    checkString = [checkString stringByReplacingOccurrencesOfString:@" " withString:@""];

    if ([PFCaculator isPureFigure:checkString]) {
        return YES;
    }
    NSString *pattern = @"^([0-9]+([.]{1}[0-9]+){0,1}),(([0-9]+([.]{1}[0-9]+){0,1}),)*([0-9]+([.]{1}[0-9]+){0,1})$";
    NSRegularExpression *regular = [[NSRegularExpression alloc] initWithPattern:pattern options:NSRegularExpressionCaseInsensitive error:nil];
    NSArray *results = [regular matchesInString:checkString options:0 range:NSMakeRange(0, checkString.length)];
    NSLog(@"%@ %ld", checkString, results.count);
    if (results.count == 0) {
        return NO;
    }else{
        return YES;
    }
}


/// 是否是纯数字
/// @param checkString 字符串
+ (BOOL)isPureFigure:(NSString *)checkString {
    checkString = [checkString stringByReplacingOccurrencesOfString:@" " withString:@""];
    if (checkString.length == 0) {
        return YES;
    }
    
    NSString *pattern = @"^[0-9]+([.]{1}[0-9]+){0,1}$";
    //1.1将正则表达式设置为OC规则
    NSRegularExpression *regular = [[NSRegularExpression alloc] initWithPattern:pattern options:NSRegularExpressionCaseInsensitive error:nil];
    //2.利用规则测试字符串获取匹配结果
    NSArray *results = [regular matchesInString:checkString options:0 range:NSMakeRange(0, checkString.length)];
    if (results.count == 0) {
        return NO;
    }else{
        return YES;
    }
}

+ (float)max:(NSString *)valueStr {
    if (![PFCaculator isDataValid:valueStr]) {
        return -1;
    }
    NSArray *array = [valueStr componentsSeparatedByString:@","];

    float max =[[array valueForKeyPath:@"@max.floatValue"] floatValue];
    return max;
    
}

+ (float)min:(NSString *)valueStr {
    if (![PFCaculator isDataValid:valueStr]) {
        return -1;
    }
    NSArray *array = [valueStr componentsSeparatedByString:@","];
    
    float min =[[array valueForKeyPath:@"@min.floatValue"] floatValue];
    return min;
}

@end
