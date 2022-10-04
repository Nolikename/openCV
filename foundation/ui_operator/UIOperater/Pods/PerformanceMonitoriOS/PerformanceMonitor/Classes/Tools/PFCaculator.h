//
//  Caculator.h
//  NextTestDylib
//
//  Created by ihenryhuang(黄洪) on 2020/11/8.
//  Copyright © 2020 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/**
 计算values的平均值的计算器
 */
@interface PFCaculator : NSObject

/// 计算平均值
/// @param valueStr 值
+ (float)avg:(NSString *)valueStr;

/// 计算最大值
/// @param valueStr 值
+ (float)max:(NSString *)valueStr;

/// 计算最小值
/// @param valueStr 值
+ (float)min:(NSString *)valueStr;

@end

NS_ASSUME_NONNULL_END
