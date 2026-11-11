#pragma once
#include <vector>
#include <string>
#include <cmath>
#include <cstdlib>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class ResourceAllocator {
public:
    static std::string select_node(const json& nodes, const json& vm, const std::string& strategy) {
        std::string selected_id = "";
        long best_score = -1;
        bool first = true;

        for (const auto& node : nodes) {
            int avail_cpu = node["total_cpu"].get<int>() - node["used_cpu"].get<int>();
            int avail_ram = node["total_ram"].get<int>() - node["used_ram"].get<int>();
            int avail_storage = node["total_storage"].get<int>() - node["used_storage"].get<int>();

            if (avail_cpu >= vm["cpu"].get<int>() && 
                avail_ram >= vm["ram"].get<int>() && 
                avail_storage >= vm["storage"].get<int>()) {
                
                long current_score = 0;
                if (strategy == "first_fit") {
                    return node["id"].get<std::string>();
                } else if (strategy == "best_fit") {
                    current_score = avail_cpu + avail_ram + avail_storage;
                    if (first || current_score < best_score) {
                        best_score = current_score; selected_id = node["id"].get<std::string>();
                    }
                } else if (strategy == "worst_fit") {
                    current_score = avail_cpu + avail_ram + avail_storage;
                    if (first || current_score > best_score) {
                        best_score = current_score; selected_id = node["id"].get<std::string>();
                    }
                } else if (strategy == "balanced") {
                    double cpu_util = (double)(node["used_cpu"].get<int>() + vm["cpu"].get<int>()) / node["total_cpu"].get<int>();
                    double ram_util = (double)(node["used_ram"].get<int>() + vm["ram"].get<int>()) / node["total_ram"].get<int>();
                    current_score = (long)(std::abs(cpu_util - ram_util) * 1000);
                    
                    if (first || current_score < best_score) {
                        best_score = current_score; selected_id = node["id"].get<std::string>();
                    }
                }
                first = false;
            }
        }
        return selected_id;
    }
};