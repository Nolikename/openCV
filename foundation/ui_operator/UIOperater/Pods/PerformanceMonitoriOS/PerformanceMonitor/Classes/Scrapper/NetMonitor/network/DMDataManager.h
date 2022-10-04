//
//  DMDataManager.h
//  Liuliang
//
//  Created by ihenryhuang(黄洪) on 2020/4/8.
//  Copyright © 2020 Tencent. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "DMNetworkTrafficLog.h"

NS_ASSUME_NONNULL_BEGIN

@interface DMDataManager : NSObject

@property(nonatomic, assign) long long int totalRev;
@property(nonatomic, assign) long long int totalSend;

+ (DMDataManager *)defaultDB;

- (void)addNetworkTrafficLog:(DMNetworkTrafficLog *)log;

@end

NS_ASSUME_NONNULL_END
