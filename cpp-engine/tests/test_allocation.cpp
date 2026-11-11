#include <gtest/gtest.h>
#include "allocator.hpp"

TEST(AllocationTest, FirstFit) {
    json nodes = json::array({
        {{"id", "node-1"}, {"total_cpu", 16}, {"used_cpu", 4}, {"total_ram", 32768}, {"used_ram", 8192}, {"total_storage", 100}, {"used_storage", 20}},
        {{"id", "node-2"}, {"total_cpu", 32}, {"used_cpu", 0}, {"total_ram", 65536}, {"used_ram", 0}, {"total_storage", 200}, {"used_storage", 0}}
    });
    json vm = {{"cpu", 4}, {"ram", 8192}, {"storage", 10}};
    
    std::string result = ResourceAllocator::select_node(nodes, vm, "first_fit");
    EXPECT_EQ(result, "node-1"); // Should pick the first available
}

TEST(AllocationTest, BestFit) {
    json nodes = json::array({
        {{"id", "large"}, {"total_cpu", 32}, {"used_cpu", 0}, {"total_ram", 65536}, {"used_ram", 0}, {"total_storage", 200}, {"used_storage", 0}},
        {{"id", "small"}, {"total_cpu", 8}, {"used_cpu", 0}, {"total_ram", 16384}, {"used_ram", 0}, {"total_storage", 50}, {"used_storage", 0}}
    });
    json vm = {{"cpu", 4}, {"ram", 8192}, {"storage", 10}};
    
    std::string result = ResourceAllocator::select_node(nodes, vm, "best_fit");
    EXPECT_EQ(result, "small"); // Should pick the smallest node that fits
}