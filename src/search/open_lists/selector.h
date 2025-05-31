#ifndef DIV_SELECTOR_H
#define DIV_SELECTOR_H

#include <deque>
#include "./div_tiebreaking_open_list.h" // for the enums
#include <optional>
#include <vector>
using std::deque;

template<class Entry>
class Selector {

    int counter;
    int number_of_entries;
    int max_depth;
    int depth_width;

    using DepthBucket = deque<Entry>;
    deque<DepthBucket> depth_bucket_list;

public:
    Selector()
        : counter(-1), number_of_entries(0), max_depth(0), depth_width(0) {
    }

    Entry remove_next(div_tiebreaking_open_list::TieBreakingCriteria tiebreaking_criteria) {
        if (empty()) {
            std::cerr << "Selector::remove_next() called on empty Selector" << std::endl;
            exit(1);
        }

        if (counter == -1) {
            if (depth_bucket_list.empty()) {
                std::cerr << "depth_bucket_list is currently empty" << std::endl;
            } else {
                rewind_counter();
            }
        }

        if (counter < 0) { // no non-empty bucket found
            std::cerr << "All DepthBuckets are currently empty" << std::endl;
            exit(1);
        }

        //std::cout << "Bucket count: " << depth_bucket_list.size() << ", current counter: " << counter << std::endl;
        //for (size_t i = 0; i < depth_bucket_list.size(); ++i) {
        //    std::cout << "  Depth " << i << ": size = " << depth_bucket_list[i].size() << std::endl;
        //}

        std::optional<Entry> result;

        switch(tiebreaking_criteria) {
            case div_tiebreaking_open_list::TieBreakingCriteria::FIFO: {
                result = depth_bucket_list[counter].front(); // Tiebreaking inside DepthBucket is FIFO
                depth_bucket_list[counter].pop_front();
                break;
            }
            case div_tiebreaking_open_list::TieBreakingCriteria::LIFO: {
                result = depth_bucket_list[counter].back(); // Tiebreaking inside DepthBucket is LIFO
                depth_bucket_list[counter].pop_back();
                break;
            }
            case div_tiebreaking_open_list::TieBreakingCriteria::RANDOM: {
                srand(time(nullptr));
                int pos;
                int i;
                i = depth_bucket_list[counter].size();
                pos = (rand() % i);

                auto it = depth_bucket_list[counter].begin();
                std::advance(it, pos);
                result = *it;
                depth_bucket_list[counter].erase(it);
                break;
            }
            default: {
                std::cout << "Tie-breaking criteria was not found. Using default FIFO." << std::endl;
                result = depth_bucket_list[counter].front(); // Tiebreaking inside DepthBucket is FIFO
                depth_bucket_list[counter].pop_front();
            }
        }
        --number_of_entries;
        //std::cout << "Number of entries after remove_next() in selector : " << number_of_entries << std::endl;
        decrease_counter();


        if (!result.has_value()) {
            std::cerr << "ERROR: result has no value!" << std::endl;
            exit(1);
        }

        if constexpr (std::is_same<Entry, StateID>::value) {
            if (*result == StateID::no_state) {
                std::cerr << "ERROR: Selected invalid StateID (no_state)" << std::endl;
                exit(1);
            }
        }

        return *result;
    }

    std::vector<int> add(Entry entry, int d_value) {
        if (depth_bucket_list.size() <= d_value) {
            depth_bucket_list.resize(d_value + 1);
        }
        depth_bucket_list[d_value].push_back(entry);

        if ((depth_bucket_list.size() - 1) > max_depth) { // updates maximal depth that has been reached until this point
            max_depth = (depth_bucket_list.size() - 1);
        }

        if (depth_bucket_list[d_value].size() > depth_width) { // updates the size of the depthbuckets aka. the width of a depth level
            depth_width = depth_bucket_list[d_value].size();
        }

        ++number_of_entries;
        //std::cout << "Number of entries after add in selector : " << number_of_entries << std::endl;
        std::vector<int> max_values = {number_of_entries, max_depth, depth_width};
        return max_values;
    }

    bool empty() {
        for (const auto &bucket : depth_bucket_list) {
            if (!bucket.empty())
                return false;
        }
        return true;
    }

protected:
    void decrease_counter() {
        while (depth_bucket_list[counter].empty() && number_of_entries > 0) {
            --counter;
            if (counter < 0) {
                rewind_counter();
            }
        }
        if (counter < 0) {
            rewind_counter();
        }
    }

    void rewind_counter() {
        if (depth_bucket_list.empty()) {
            counter = 0;
            return;
        } else {
            for (int i = depth_bucket_list.size() - 1; i >= 0; --i) { // goes over all DepthBuckets and finds deepest non-empty one
                if (!depth_bucket_list[i].empty()) {
                    counter = i;
                    return;
                }
            }
        }
        counter = 0;
    }
};


#endif
