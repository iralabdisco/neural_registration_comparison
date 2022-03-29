#ifndef COMPARISON_UTILITY_PCD_UTILS
#define COMPARISON_UTILITY_PCD_UTILS
#include <string>
#include <vector>
#include <iostream>

void tokenize(std::string const &str, const char* delim, 
            std::vector<std::string> &out) 
{ 
    char *token = strtok(const_cast<char*>(str.c_str()), delim); 
    while (token != NULL) 
    { 
        out.push_back(std::string(token)); 
        token = strtok(NULL, delim); 
    } 
} 

bool is_valid(float x){
  return !std::isnan(x) && !std::isinf(x);
}

int read_pcd(std::string filename, std::vector<float>& pts){
  std::ifstream pointcloud_file(filename.c_str());
  if (!pointcloud_file) {
    std::cerr << "Point cloud file not found." << std::endl;
    return -1;
  }
  int num_pts = 0;
  bool data = false;
  std::string line_str;
  while (std::getline(pointcloud_file, line_str)) {
    std::vector<std::string> split; 
    tokenize(line_str, " ", split); 
    if(split[0] == "POINTS"){
      num_pts = std::stoi(split[1]);
    }
    else if(split[0] == "DATA"){
      data = true;
    }
    else if(data){
        float x = std::stof(split[0]);
        float y = std::stof(split[1]);
        float z = std::stof(split[2]);
        if(is_valid(x) && is_valid(y) && is_valid(z)){
          pts.push_back(x);
          pts.push_back(y);
          pts.push_back(z);
        }
        else{
          num_pts--;
        }
    }
  }

  if (num_pts == 0) {
    std::cerr << "Empty point cloud" << std::endl;
    return 0;
  }
  pointcloud_file.close();

  assert(num_pts == pts.size()/3);
  return num_pts;
}


#endif /* COMPARISON_UTILITY_PCD_UTILS */
